// Import React stuff
import React from "react";
import ReactDOM from "react-dom";
import * as Icon from 'react-feather';

import client from './api';
import { ErrorBoundary } from './errorboundary';

const categories = ['Green Machines', 'Metal Working'];

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tab: 'tools'
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
                <Nav switchTab={this.switchTab} tab={this.state.tab} />
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
            <nav class="AdminNav">
                <ul>
                    <li className={"AdminNav__tab  " + (this.props.tab == 'administration' ? 'AdminNav__tab--current' : '')}><a href="#" onClick={() => this.changeTab('administration')}>Administration</a></li>
                    <li className={"AdminNav__tab  " + (this.props.tab == 'tools' ? 'AdminNav__tab--current' : '')}><a href="#" onClick={() => this.changeTab('tools')}>Tools</a></li>
                    <li className={"AdminNav__tab  " + (this.props.tab == 'users' ? 'AdminNav__tab--current' : '')}><a href="#" onClick={() => this.changeTab('users')}>Users</a></li>
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

        this.state = {
            ready: false,
        }
    }

    componentDidMount() {
        client.get('/api/tools/')
        .then(res => {
            console.log(res);
            this.setState({
                ready: true,
                tools: res.data
            })
        })
        .catch(err => {
            console.log(err);
            throw new Error(err)
        })
    }

    render() {
        return (
            <>
                <details className="AddFormWrapper">
                    <summary className="AddFormWrapper__button">Add Tool</summary>
                    <ToolForm />
                </details>
                {this.state.ready ? <ToolList tools={this.state.tools} /> : "Loading..."}
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

        for (var element of form.entries()) {
            var name = element[0];
            var value = element[1];

            if (!value) {
                alert("You are missing one or more values: " + name);
                return;
            }
        }

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
            <form className="AddForm" id="toolForm" enctype="multipart/form-data" method="post">
                <label for="name" className="AddForm__input">
                    <span className="AddForm__input__label">Name</span>
                    <input required type="text" name="name" id="name" />
                </label>

                <label for="shortname" className="AddForm__input">
                    <span className="AddForm__input__label">Short Name</span>
                    <input required type="text" name="shortname" id="shortname" />
                </label>

                <label for="category" className="AddForm__input">
                    <span className="AddForm__input__label">Category</span>
                    <select required name="category" id="category">
                        <option value="">Select one</option>
                        {categoryOptions}
                    </select>
                </label>

                <button type="button" onClick={() => this.handleSubmit()}>Submit</button>
            </form>
        )
    }
}

class ToolList extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        var tools = this.props.tools.map(tool => {
            return <ToolListing tool={tool} />;
        })
        return (
            <table className="ToolsTable">
                <thead className="ToolsTable__head">
                    <tr>
                        <th className="ToolsTable__head__cell">Tool</th>
                        <th className="ToolsTable__head__cell">Category</th>
                        <th className="ToolsTable__head__cell">Short Name</th>
                    </tr>
                </thead>
                <tbody className="ToolsTable__body">
                    {tools}
                </tbody>

            </table>
        )
    }
}

class ToolListing extends React.Component {
    constructor(props) {
        super(props);

        this.deleteTool = this.deleteTool.bind(this);
        this.editTool = this.editTool.bind(this);
        this.finishEdit = this.finishEdit.bind(this);
        this.cancelEdit = this.cancelEdit.bind(this);

        this.state = {
            editing: false,
            tool: this.props.tool,
        }
    }

    deleteTool(e) {
        e.stopPropagation();
        e.preventDefault();
        if (window.confirm("Are you sure you want to delete this tool?")) {
            console.log(this.props.tool.id);
        }
    }

    editTool() {
        this.setState({editing: true});
    }

    cancelEdit() {
        this.setState({editing: false});
    }

    finishEdit() {
        this.setState({editing: false});
    }

    render() {
        if (this.state.editing) {
            const categoryOptions = categories.map(category => <option value={category}>{category}</option>);

            return (
                <tr className="ToolListing">
                    <td className="ToolListing__name"><input type="text" defaultValue={this.state.tool.name} /></td>
                    <td className="ToolListing__category"><select defaultValue={this.state.tool.category.name}>{categoryOptions}</select></td>
                    <td className="ToolListing__shortname"><input type="text" defaultValue={this.state.tool.shortname} /></td>
                    <td className="ToolListing__edit-button"><button onClick={this.finishEdit} value={this.state.tool.id}><Icon.Check color="green" /></button></td>
                    <td className="ToolListing__delete-button"><button onClick={this.cancelEdit} value={this.state.tool.id}><Icon.X color="red" /></button></td>
                </tr>
            )
        } else {
            return (
                <tr className="ToolListing">
                    <td className="ToolListing__name">{this.state.tool.name}</td>
                    <td className="ToolListing__category">{this.state.tool.category.name}</td>
                    <td className="ToolListing__shortname">{this.state.tool.shortname}</td>
                    <td className="ToolListing__edit-button"><button onClick={this.editTool} value={this.state.tool.id}><Icon.Edit /></button></td>
                    <td className="ToolListing__delete-button"><button onClick={this.deleteTool} value={this.state.tool.id}><Icon.Trash2 color="red" /></button></td>
                </tr>
            )
        }
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
