import { ReactWidget } from '@jupyterlab/apputils';
import Tabs from './Tabs';

export class CounterWidget extends ReactWidget {
  constructor() {
    super();
    this.addClass('dla-Container');
  }

  render(): JSX.Element {
    return <Tabs />
  }
}
