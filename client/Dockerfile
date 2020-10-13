FROM node:10.16.0-alpine

WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

#start the development server
CMD ["npm", "start"]