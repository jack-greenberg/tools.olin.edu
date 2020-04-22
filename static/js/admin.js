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
                ADD FORM
                <ToolForm />
            </>
        )
    }
}

class ToolForm extends React.Component {
    constructor(props) {
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this);

        this.categories = ['Green Machines', 'Metal Working']; // TODO: Fill this in as a prop from site data from database
    }

    handleSubmit() {
        var formElement = document.getElementById('toolForm');
        var form = new FormData(formElement);

        client.post('/api/tools/', form)
        .then(res => {
            console.log(res)
        })
        .catch(err => {
            console.log(err)
        })
    }

    render() {
        const categoryOptions = this.categories.map(category => <option value={category}>{category}</option>);
        return (
            <form id="toolForm" enctype="multipart/form-data" method="post">
                <label for="name">
                    Name
                    <input required type="text" name="name" id="name" />
                </label>

                <label for="shortname">
                    Short Name
                    <input required type="text" name="shortname" id="shortname" />
                </label>

                <label for="category">
                    Category
                    <select required name="category" id="category">
                        <option value="NULL">Select one</option>
                        {categoryOptions}
                    </select>
                </label>

                <button type="button" onClick={() => this.handleSubmit()}>Submit</button>
            </form>
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
