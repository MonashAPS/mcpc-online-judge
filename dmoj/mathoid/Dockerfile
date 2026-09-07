FROM node:10.21.0

# 0.7.5 is the last mathoid whose dependency tree still runs on Node 10;
# 0.7.6 pulls service-runner 3 and a commander that Node 10 cannot parse.
# speech-rule-engine declares commander "*", which now resolves to an ESM-only
# release; 7.2.0 is what the last working build had.
RUN npm install mathoid@0.7.5 commander@7.2.0 && \
    ln -sfv /node_modules/mathoid/app.js /node_modules/app.js

EXPOSE 10044
WORKDIR /node_modules/mathoid
CMD /node_modules/mathoid/server.js
