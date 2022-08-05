import streamlit as st


def html(body):
    st.markdown(body, unsafe_allow_html=True)


def card_begin_str(header):
    return (
        "<style>div.card{background-color:#D4FAFA;border-radius: 5px;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);transition: 0.3s; padding: 24px 24px 16px; margin: 10px 0}</style>"
        '<div class="card">'
        '<div class="container">'
        f"<h5>{header}</h5>"
    )


def card_end_str():
    return "</div></div>"


def card(header, body):
    lines = [card_begin_str(header), f"<p>{body}</p>", card_end_str()]
    html("".join(lines))
