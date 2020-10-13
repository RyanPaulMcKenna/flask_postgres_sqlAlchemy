import * as React from 'react';
import { IAppService } from '.';
import './App.css';


export interface IAppProps {
  service: IAppService;
}

export interface IAppState {
  data: string;
}

export class App extends React.Component<IAppProps, IAppState> {
  constructor(props: IAppProps) {
    super(props);
    this.state = {
      data: '',
    }
  }

  public async componentDidMount() {
    const data = await this.props.service.getData();
    console.log(data);
    this.setState({ data });
  }

  public render() {
    return (
      <div>
        <h1>{this.state.data}</h1>
      </div>
    );
  }
}

export default App;
