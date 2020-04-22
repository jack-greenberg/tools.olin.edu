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

        this.switchTab = this.switchTab.bind(this);
    }

    switchTab(tab) {
        this.setState({
            tab: tab,
        })
    }

    render() {
        return (
            <>
                <Nav switchTab={this.switchTab} />
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

        this.changeTab = this.changeTab.bind(this);
    }

    changeTab(tab) {
        this.props.switchTab(tab)
    }

    render() {
        return (
            <nav>
                <ul>
                    <li><a href="#" onClick={() => this.changeTab('administration')}>Administration</a></li>
                    <li><a href="#" onClick={() => this.changeTab('tools')}>Tools</a></li>
                    <li><a href="#" onClick={() => this.changeTab('users')}>Users</a></li>
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
