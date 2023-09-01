import streamlit as st
import humanize
import os
import json

from s3_browser.common import query_text_input, safe_get_query_value
from s3_browser.common.s3_client import get_s3_client
from code_editor import code_editor
from typing import List
from urllib.parse import quote


btn_settings_editor_btns = [
    {
        "name": "copy",
        "feather": "Copy",
        "hasText": True,
        "alwaysOn": False,
        "commands": ["copyAll"],
        "style": {"top": "0rem", "right": "0.4rem"},
    }
]
img_or_video_ext_list = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".mp4")

image_gallery_style = """
<style>
div.gallery {
  margin: 5px;
  border: 1px solid #ccc;
  float: left;
  width: 360px;
  height: 400px;
}

.img-container {
    width: 360px;
    height: 350px;
    overflow: hidden;
    display: table-cell;
    vertical-align: middle;
    text-align: center;
}

div.gallery:hover {
  border: 1px solid #777;
}

div.gallery img {
  width: auto;
  height: auto;
  max-width: 100%;
  max-height:100%;
}

div.desc {
  font-size: 10px;
  padding: 15px;
  text-align: center;
  width: auto;
  overflow: hidden;
}
</style>
"""

st.set_page_config(page_title="File Explorer", page_icon="📂", layout="wide")
s3_path = query_text_input("S3 Path", "s3_path")

current_s3 = safe_get_query_value("current_s3")


def write_parent(path):
    st.markdown(
        f"""
        <pre>
            <span style='display: inline-block; width: 400px;'></span>
            <a href="/Explorer?current_s3={current_s3}&s3_path={path}" target = "_self">↑PARENT↑</a>
        </pre>
        """,
        unsafe_allow_html=True,
    )


def write_item(l1, l2, l3, path, download_path=None):
    download_link = ""
    if download_path:
        download_link = f'[<a href="{download_path}">↓</a>]'

    def truncate(data):
        info = (data[:12] + '..') if len(data) > 12 else data
        return info

    st.markdown(
        f"""
        <pre>
            <span style='display: inline-block; width: 150px;'>{l1}</span>
            <span style='display: inline-block; width: 120px;'>{l2}</span>
            <span style='display: inline-block; width: 130px;'>{truncate(l3)}</span>
            <a href="/Explorer?current_s3={current_s3}&s3_path={path}" target = "_self">{path}</a>
            {download_link}
        </pre>
        """,
        unsafe_allow_html=True,
    )


if len(s3_path) == 0:
    buckets = get_s3_client().list_buckets()
    if len(buckets) == 0:
        st.error("Empty bucket list")
    else:
        for bucket in buckets:
            write_item("", "", "BUCKET", f"s3://{bucket}/")
    st.stop()


if not s3_path.startswith("s3://"):
    st.warning("invalid s3 path")
    st.stop()


def get_parent(path: str):
    parts = path.removeprefix("s3://").removesuffix("/").split("/")
    if len(parts) <= 1:
        return ""
    return "s3://" + "/".join(parts[:-1]) + "/"


def download_url(path):
    return get_s3_client().generate_presigned_url(path)


def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""


def format_size(size):
    if size is None:
        return ""
    try:
        size = int(size)
    except:
        return "NA"
    return humanize.naturalsize(size)


def write_object(obj, path):
    last_modified = obj.get("LastModified")
    size = obj.get("Size") or obj.get("ContentLength", 0)
    owner = obj.get("Owner", {}).get("ID", "")
    write_item(
        format_datetime(last_modified),
        format_size(size),
        owner,
        path,
        download_url(path),
    )


write_parent(get_parent(s3_path))


@st.cache_data(ttl="2h")
def list_objects_with_cache(s3_path, max_count):
    return list(get_s3_client().list_objects(s3_path, max_count=max_count))


def pagination(key: str, max_len: int, page_size=6) -> int:
    col1, col2, col3, col4, col5 = st.columns([1, 7, 1, 0.5, 1])
    col4.markdown(
        f"<div style='text-align: center; height: 40px; line-height: 40px;'>Size:</div>",
        unsafe_allow_html=True,
    )

    page_size = col5.number_input(
        "Page Size",
        min_value=1,
        max_value=16,
        value=page_size,
        label_visibility="collapsed",
        key="page_size_input",
    )
    total_page = int(max_len / page_size)
    if max_len % page_size != 0:
        total_page += 1

    if "page_size" not in st.session_state:
        st.session_state.page_size = page_size
    elif st.session_state.page_size != page_size:
        st.session_state[key] = 0
        st.session_state["page_size"] = page_size

    def move_index(prev=False):
        if prev:
            st.session_state[key] -= 1
            if st.session_state[key] <= 0:
                st.session_state[key] = 0
        else:
            st.session_state[key] += 1
            if st.session_state[key] >= total_page:
                st.session_state[key] = total_page - 1

    if st.session_state[key] != 0:
        col1.button("Previous", on_click=lambda: move_index(prev=True))
    col2.markdown(
        f"<div style='text-align: center; height: 40px; line-height: 40px;'>{st.session_state[key] + 1}/{total_page}</div>",
        unsafe_allow_html=True,
    )
    if st.session_state[key] != max_len - 1:
        col3.button("Next", on_click=lambda: move_index())
    return page_size


def format_image_item(s3_img: str) -> str:
    filename = os.path.basename(s3_img)
    img_url = get_s3_client().generate_presigned_url(s3_img)
    return f"""<div class="gallery">
  <a target="_blank" href="{img_url}">
    <div class="img-container">
        <img src="{img_url}">
    </div>
  </a>
  <div class="desc">{filename}</div>
</div>"""


def list_dir_in_image_mode(s3_path):
    filelist = list_current_dir_img_or_video_list(s3_path)
    filelist = [item for item in filelist if not item.lower().endswith(".mp4")]
    if len(filelist) == 0:
        st.info("No images")
        st.stop()

    if "page" not in st.session_state:
        st.session_state.page = 0
    page_size = pagination("page", len(filelist))

    current_images = filelist[
        st.session_state.page * page_size : (st.session_state.page + 1) * page_size
    ]
    st.markdown(image_gallery_style, unsafe_allow_html=True)

    img_html_content = ""
    for s3_img in current_images:
        img_html_content += format_image_item(s3_img)
    st.markdown(img_html_content, unsafe_allow_html=True)
    st.stop()


# list objects under s3_path
def list_dir(s3_path):
    max_count = 1000
    _, col2 = st.columns([10, 2])
    image_mode = col2.checkbox("Image explore mode")

    with st.spinner("Loading..."):
        if image_mode:
            list_dir_in_image_mode(s3_path)
            return

        objects = list_objects_with_cache(s3_path, max_count)
        item_count = len([path for path, _ in objects if not path.endswith("/")])

        if item_count == max_count:
            st.info(f"Only show {max_count} items.")

        for path, detail in objects:
            if path.endswith("/"):
                write_item("", "", "DIR", path)
            else:
                write_object(detail, path)


@st.cache_data(ttl="2h")
def list_current_dir_img_or_video_list(s3_path: str) -> List[str]:
    objects = list_objects_with_cache(s3_path, max_count=1000)
    return [path for path, _ in objects if path.lower().endswith(img_or_video_ext_list)]


def try_view_img_or_video(s3_path: str):
    if not s3_path.lower().endswith(img_or_video_ext_list):
        return

    parent = get_parent(s3_path)
    filelist = list_current_dir_img_or_video_list(parent)
    has_index = False

    if s3_path in filelist:
        has_index = True

    if has_index:
        current_index = filelist.index(s3_path)
        col1, col2, col3 = st.columns([1, 10, 1])
        next_index = current_index + 1
        if next_index >= len(filelist):
            next_index = len(filelist) - 1

        prev_index = current_index - 1
        if prev_index <= 0:
            prev_index = 0

        if current_index != 0:
            col1.markdown(
                f"<a href='/Explorer?current_s3={current_s3}&s3_path={quote(filelist[prev_index])}' target='_self'>Previous</a>",
                unsafe_allow_html=True,
            )
        col2.markdown(
            f"<div style='text-align: center;'>{current_index + 1}/{len(filelist)}</div>",
            unsafe_allow_html=True,
        )
        if current_index != len(filelist) - 1:
            col3.markdown(
                f"<a href='/Explorer?current_s3={current_s3}&s3_path={quote(filelist[next_index])}' target='_self'>Next</a>",
                unsafe_allow_html=True,
            )

    url = get_s3_client().generate_presigned_url(s3_path)
    if s3_path.lower().endswith(".mp4"):
        st.video(url)
    else:
        st.image(url, width=800)
    st.stop()


@st.cache_data(ttl="2h")
def read_file_content(s3_path, read_size):
    obj_body = get_s3_client().read_object(s3_path, f"0,{read_size}")
    content: bytes = obj_body.read()
    return content


def try_view_jsonl(text: str, read_size, size):
    lines = text.splitlines()
    if read_size < size and len(lines) > 1:
        # drop last line incase it is truncated.
        lines = lines[:-1]

    if "jsonl_page_index" not in st.session_state:
        st.session_state.jsonl_page_index = 0

    formatted_lines = []
    for line in lines:
        try:
            json_data = json.loads(line)
            formatted_lines.append(json.dumps(json_data, ensure_ascii=False, indent=4))
        except Exception:
            pass

    page_size = pagination("jsonl_page_index", len(formatted_lines), 1)
    begin_idx = page_size * st.session_state.jsonl_page_index
    end_idx = begin_idx + page_size
    for i in range(begin_idx, end_idx):
        if i >= len(formatted_lines):
            continue

        st.write(f"### Line {i+1}")
        st.json(formatted_lines[i])
    st.stop()


def try_view_text_file(s3_path: str, head_resp):
    size = head_resp.get("ContentLength", 0)
    read_size = min(size, 1 << 20)
    if not read_size:
        st.info("File is empty.")
        st.stop()

    with st.spinner("Reading..."):
        with st.columns([1, 5, 1])[2]:
            st.button(
                "Clear cached content", on_click=lambda: read_file_content.clear()
            )
        content: bytes = read_file_content(s3_path, read_size)

        try:
            text = content.decode("utf-8", errors="ignore")
        except Exception as e:
            st.error("Error Occurred.")
            st.stop()

    if not len(text):
        st.info("File is empty.")
        st.stop()

    if read_size < size:
        info_texts = f"Only read {read_size} bytes."
        st.info(info_texts)

    extension_to_language = {
        (".md"): "markdown",
        (".sh", ".txt"): "text",
        (".json"): "json",
        # add more
    }

    for ext, lang in extension_to_language.items():
        if s3_path.endswith(ext):
            if lang == "json" and read_size == size:
                st.json(text)
            else:
                code_editor(
                    text,
                    lang=lang,
                    buttons=btn_settings_editor_btns,
                    height=24,
                    options={"wrap": True},
                )
            st.stop()

    if s3_path.lower().endswith(".jsonl"):
        try_view_jsonl(text, read_size, size)


def show_file(s3_path):
    head_resp = get_s3_client().head_object(s3_path)
    write_object(head_resp, s3_path)

    # will st.stop if viewable
    try_view_img_or_video(s3_path)
    try_view_text_file(s3_path, head_resp)


is_file = get_s3_client().is_file(s3_path)
if not is_file:
    list_dir(s3_path)
else:
    show_file(s3_path)
