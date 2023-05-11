mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"maggiema0326@gmail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]
base="light"
primaryColor="#2d753a"
secondaryBackgroundColor="#748dbf"
textColor="#141313"
" > ~/.streamlit/config.toml
