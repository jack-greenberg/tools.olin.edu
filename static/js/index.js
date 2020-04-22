// Import styles so webpack will compile them into build.css
import "../css/index.scss";

// Import React stuff
import React from "react";
import ReactDOM from "react-dom";

// App
import Training from './training'

import client from './api';
import { ErrorBoundary } from './errorboundary';

export const AppContext = React.createContext({});

class App extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        var tool = window.location.pathname.split('/');
        tool = tool[tool.length - 1];

        return <Training tool={tool} />;
    };
};

var renderedApp = (
    <ErrorBoundary>
        <App />
    </ErrorBoundary>
);

ReactDOM.render(renderedApp, document.getElementById('root'));
