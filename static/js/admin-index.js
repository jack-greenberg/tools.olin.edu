// Import React stuff
import React from "react";
import ReactDOM from "react-dom";

import client from './api';
import { ErrorBoundary } from './errorboundary';

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tab: 'administration'
        }

        this.tab = {
            administration: <Administration />,
            tools: <Tools />,
            users: <Users />
        }
    }
    render() {
        return (
            <>
                <Nav />
                <main>
                    {this.tab[this.state.tab]}
                </main>
            </>
        )
    };
};

class Nav extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <nav>
                <ul>
                    <li><a>Administration</a></li>
                    <li><a>Tools</a></li>
                    <li><a>Users</a></li>
                </ul>
            </nav>
        )
    }
}

class Administration extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <>
                Administration Section
            </>
        )
    }
}

class Tools extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <>
                Tools Section
            </>
        )
    }
}

class Users extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <>
                Users Section
            </>
        )
    }
}

var renderedApp = (
    <ErrorBoundary>
        <App />
    </ErrorBoundary>
);

ReactDOM.render(renderedApp, document.getElementById('root'));
