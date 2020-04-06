// Import Styles
import './index.scss';

// Import React stuff
import React from 'react-js';
import ReactDOM from 'react-dom';
import { Provider, connect } from 'react-redux';
import { ErrorBoundary } from './errorboundary';

export const AppContext = React.createContext({});

class App extends React.Component {
    constructor(props) {
        super(props);
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
