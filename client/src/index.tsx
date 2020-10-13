import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';


export interface IHelloData {
  status: string;
  users: [];
}

export interface IAppService {
  getData(): Promise<string>
}

export class AppService implements IAppService {
  public async getData() {
    return fetch('/app', {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
      credentials: 'same-origin',
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`${response.status}${response.text}`);
        }
        const payload: IHelloData = await response.json();
        return payload.status;
      })
      .catch((reason) => {
        if (reason instanceof Error) {
          throw reason;
        }
        throw new Error(reason);
      });
  }
}


const service: IAppService = new AppService();

ReactDOM.render(
  <React.StrictMode>
    <App service={service} />
  </React.StrictMode>, document.getElementById('root')
);



// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
