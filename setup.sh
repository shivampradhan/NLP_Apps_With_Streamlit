mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"shivampradhan2025@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\