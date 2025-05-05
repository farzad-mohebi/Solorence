# use node 16 alpine image
FROM node:20-alpine

ARG BACKEND_URL
ARG GOOGLE_CLIENT_ID

ENV BACKEND_URL=${BACKEND_URL}
ENV GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}

# create work directory in app folder
WORKDIR /usr/src/front

# install required packages for node image
RUN apk --no-cache add openssh g++ make python3 git

# copy over package.json files
COPY ./front/package.json .
COPY ./front/package-lock.json .

# install all depencies
RUN npm ci && npm cache clean --force

# copy over all files to the work directory
ADD ./front .

# build the project
RUN npm run build

# expose the host and port 3000 to the server
ENV HOST 0.0.0.0
EXPOSE 3000

# run the build project with node
ENTRYPOINT ["node", "/usr/src/front/.output/server/index.mjs"]


