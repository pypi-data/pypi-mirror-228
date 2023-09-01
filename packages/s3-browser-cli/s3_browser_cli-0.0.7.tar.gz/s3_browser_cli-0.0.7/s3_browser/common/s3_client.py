import boto3
import re

from typing import List, Union
import streamlit as st
from s3_browser.common import safe_get_query_value


__re_s3_path = re.compile("^s3a?://([^/]+)(?:/(.*))?$")


def split_s3_path(path: str):
    "split bucket and key from path"
    m = __re_s3_path.match(path)
    if m is None:
        return "", ""
    return m.group(1), (m.group(2) or "")


class S3Client:
    def __init__(self, ak, sk, endpoint, name=""):
        self.cli = boto3.client(
            "s3", aws_access_key_id=ak, aws_secret_access_key=sk, endpoint_url=endpoint
        )
        self.ak = ak
        self.endpoint_url = endpoint
        self.name = name

    def write_object(self, s3_path: str, body: bytes):
        bucket, key = split_s3_path(s3_path)
        return self.cli.put_object(Bucket=bucket, Key=key, Body=body)

    def list_objects(self, s3_path, max_count=1000, recursive=False):
        if not s3_path.endswith("/"):
            s3_path += "/"
        bucket, prefix = split_s3_path(s3_path)

        marker = None
        total_count = 0
        while True:
            list_kwargs = dict(MaxKeys=1000, Bucket=bucket, Prefix=prefix)
            if marker:
                list_kwargs["Marker"] = marker
            if not recursive:
                list_kwargs["Delimiter"] = "/"
            response = self.cli.list_objects(**list_kwargs)
            if not recursive:
                for cp in response.get("CommonPrefixes", []):
                    yield (f"s3://{bucket}/{cp['Prefix']}", cp)

            contents = response.get("Contents", [])
            should_quit = False
            for content in contents:
                total_count += 1
                if total_count > max_count:
                    should_quit = True
                    break

                if not content["Key"].endswith("/"):
                    yield (f"s3://{bucket}/{content['Key']}", content)

            if should_quit or not response.get("IsTruncated") or len(contents) == 0:
                break
            marker = contents[-1]["Key"]

    def list_buckets(self) -> List[str]:
        resp = self.cli.list_buckets()
        buckets = map(lambda b: b["Name"], resp.get("Buckets", []))
        buckets = list(buckets)
        try:
            buckets.remove("[default]")
        except ValueError:
            pass

        buckets.sort()
        return buckets

    def is_file(self, s3_path) -> bool:
        return self.head_object(s3_path) is not None

    def head_object(self, s3_path):
        bucket, key = split_s3_path(s3_path)
        try:
            resp = self.cli.head_object(Bucket=bucket, Key=key)
            return resp
        except Exception:
            return None

    def generate_presigned_url(self, s3_path: str) -> str:
        bucket, key = split_s3_path(s3_path)
        return self.cli.generate_presigned_url(
            "get_object", {"Bucket": bucket, "Key": key}
        )

    def read_object(self, s3_path, bytes: Union[str, None] = None):
        __re_bytes = re.compile("^([0-9]+)([,-])([0-9]+)$")
        bucket, key = split_s3_path(s3_path)
        kwargs = {}
        if bytes:
            m = __re_bytes.match(bytes)
            if m is not None:
                frm = int(m.group(1))
                to = int(m.group(3))
                sep = m.group(2)
                if sep == ",":
                    to = frm + to - 1
                kwargs["Range"] = f"bytes={frm}-{to}"

        return self.cli.get_object(Bucket=bucket, Key=key, **kwargs)["Body"]

    def get_bucket_policy(self, s3_path):
        bucket, _ = split_s3_path(s3_path)
        return self.cli.get_bucket_policy(Bucket=bucket)


_s3_client_map = {}

if "S3" in st.secrets:
    _s3_config = st.secrets["S3"]
    _s3_client_map["_default"] = S3Client(
        _s3_config["AK"], _s3_config["SK"], _s3_config["ENDPOINT_URL"], "_default"
    )

if "S3_Servers" in st.secrets:
    for k, v in st.secrets["S3_Servers"].items():
        _s3_client_map[k] = S3Client(v["AK"], v["SK"], v["ENDPOINT_URL"], k)


def get_s3_client() -> S3Client:
    if len(_s3_client_map) <= 0:
        st.error("no s3 config")
        st.stop()

    current_s3 = safe_get_query_value("current_s3")
    if current_s3 == "" or len(_s3_client_map) == 1:
        return list(_s3_client_map.values())[0]
    return _s3_client_map[current_s3]


def get_s3_client_list():
    return [
        {"name": v.name, "endpoint_url": v.endpoint_url, "ak": v.ak}
        for k, v in _s3_client_map.items()
    ]
