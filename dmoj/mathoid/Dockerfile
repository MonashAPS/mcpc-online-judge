FROM node:10.21.0

# 0.7.5 is the last mathoid whose dependency tree still runs on Node 10;
# 0.7.6 pulls service-runner 3 and a commander that Node 10 cannot parse.
RUN npm install mathoid@0.7.5 && \
    ln -sfv /node_modules/mathoid/app.js /node_modules/app.js

EXPOSE 10044
WORKDIR /node_modules/mathoid
CMD /node_modules/mathoid/server.js
