import styles from '../css/index.scss';

import React from 'react';
import ReactDOM from 'react-dom';
// import Router from './router';

import client from './jwt';
import { ErrorBoundary } from './errorboundary';

export const AppContext = React.createContext({});

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: siteData, //! This is set in admin.j2, in the script with `const siteData = {{ siteData|tojson }}`
        }
    }
    render() {
        return (
            <AppContext.Provider value={this.state.data}>
                <Router />
            </AppContext.Provider>
        );
    };
};

var renderedApp = (
    <ErrorBoundary>
        <App />
    </ErrorBoundary>
);

ReactDOM.render(renderedApp, document.getElementById("root"));
