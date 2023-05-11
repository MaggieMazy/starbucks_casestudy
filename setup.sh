mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"maggiema0326@gmail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\\n\
[theme]\n\
base=\"light\"\n\
primaryColor=\"#2d753a\"\n\
secondaryBackgroundColor=\"#748dbf\"\n\
textColor=\"#141313\"\n\
" > ~/.streamlit/config.toml
