# Documents
This is define rules when access documents and update them

[ ] Document must self-single html files
[ ] With miniumum style (less css)
[ ] We have the table of content html file for access other documents `table-of-contents.html`
[ ] Can access docs via run a simple server in docs folder `cd docs && python3 -m http.server 8888`

# The goal of this project [SC Chatbot] (Social Commerce Chatbot)
This a production project for e-business.
It sale a solution chatbot for SME (Small and Medium Enterprise)
This chatbot can be easy integrate with any enterprise. Give them:
1. A real chatbot can support their customer support
2. Or a chatbot for internal use with can give massive of helps for analysis the data
3. Integrate for social channel like Zalo FQA, Facebook, Instagram

## The Architecture
**Source code**
- Backend: place on `src/backend`. Use python is a main language
- Frontend: place on `src/frontend`. Use React framework
- Use nFRM to build deb, rpm package
- Have a *Makefile* for building & develop & other tager for packaging

**Backend side**
1. Can talk to LLM model via APIs like (Ollama local, Open APIs, Open Router, ...)
2. Store data of enterprise company via webhook
3. Support MCP server for other AI agent can access
4. Support tools calling for LMM when call chatbot
5. Support integrate with Zalo FQA
6. Support integrate with Facebook, other social channel (Support later)
7. User-roles based for each company & admin of this SC Chatbot
8. Deploy on cloud

**Fontend side**
1. Use a enterprice CSS

**Deploy**
1. This project support only linux
2. Build bundle to *.rpm, *.deb package
3. The process will be run as systemd service
4. Or deploy via container we also ship the Dockerfile

## The features
**TDB**