import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post


def main():
    st.subheader("LinkedIn Post Generator: By Sahaj")

    fs = FewShotPosts()
    
    # Get dynamic options from actual data
    tags = fs.get_tags()
    languages = fs.get_languages()
    length_options = ["Short", "Medium", "Long"]

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_tag = st.selectbox("Topic", options=sorted(tags))

    with col2:
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        selected_language = st.selectbox("Language", options=languages)


    if st.button("Generate"):
        post = generate_post(selected_length, selected_language, selected_tag)
        st.write(post)



if __name__ == "__main__":
    main()