import React from 'react';
import { client } from './api';
import * as Icon from 'react-feather';

export default class Training extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            permissions: 'student',
            ready: false,
        }

        this.training_id = window.location.pathname.split('/').pop();
    }

    componentDidMount() {
        client.get('/api/trainings/' + this.training_id)
        .then(res => {
            console.log(res)
            this.setState({
                data: res.data,
                trainee: res.data.trainee,
                tool: res.data.tool,
                ready: true,
            })
        })
        .catch(err => {
            console.log(err);
            this.setState({
                ready: true,
            })
        })
    }

    render() {
        if (!this.state.ready) {
            return (
                <div>
                    Loading your information...
                </div>
            )
        } else {
            return (
                <main className="Page">
                    <header className="Page__header">
                        <h1 className="Page__header__title">{this.state.tool.name} Training Checklist</h1>
                    </header>
                    <Checklist permissions={this.state.permissions} />
                </main>
            )
        }
    }
}

class Checklist extends React.Component {
    constructor(props) {
        super(props);

        this.handleCheck = this.handleCheck.bind(this);

        this.state = {
            permissions: this.props.permissions,
            disabledList: {
                reading: false,
                worksheet: true,
                training: true,
                testpiece: true
            }
        }
    }
    handleCheck(e) {
        var oldList = this.state.disabledList;

        switch(e.target.name) {
            case 'reading':
                oldList.worksheet = !e.target.checked;
                break;
            case 'worksheet':
                oldList.training = !e.target.checked;
                break;
            case 'training':
                oldList.testpiece = !e.target.checked;
                break;
            case 'testpiece':
                // Show rest of the form
                break;
        }

        this.setState({
            disabledList: oldList,
        })
    }

    render() {
        const ninja = (this.state.permissions == 'ninja');

        return (
            <>
                <form>
                    <section className="Checklist">
                        <ChecklistItem disabled={this.state.disabledList.reading} name="reading" handleCheck={this.handleCheck}>
                            Completed <a href="#">Readings</a>
                        </ChecklistItem>

                        <ChecklistItem disabled={this.state.disabledList.worksheet} name="worksheet" handleCheck={this.handleCheck}>
                            Completed <a href="#">Worksheet</a>
                        </ChecklistItem>

                        <ChecklistItem disabled={this.state.disabledList.training} name="training" handleCheck={this.handleCheck}>
                            Completed Training
                        </ChecklistItem>

                        <ChecklistItem disabled={this.state.disabledList.testpiece} name="testpiece" handleCheck={this.handleCheck}>
                            Completed Test Piece
                        </ChecklistItem>
                    </section>

                    <AuthorizeButton label="Trainer Approval" disabled={true} />

                    <ChecklistItem disabled={false} name="agreement" handleCheck={this.handleCheck}>
                        I agree to the terms and conditions.
                    </ChecklistItem>
                </form>
            </>
        )
    }
}

class ChecklistItem extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="Checkbox">
                <label className="Checkbox__flex">
                    <input style={{display: 'none'}} className="Checkbox__input" name={this.props.name} type="checkbox" defaultChecked={false} onChange={this.props.handleCheck} disabled={this.props.disabled} />
                    <span className="Checkbox__icon">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            >
                            <polyline points="20 6 9 17 4 12" />
                        </svg>
                    </span>
                    <span className="Checkbox__label">{this.props.children}</span>
                </label>
            </div>
        )
    }
}

class AuthorizeButton extends React.Component {
    constructor(props) {
        super(props);

        this.authorize = this.authorize.bind(this);
    }

    authorize() {

    }

    render() {
        return (
            <>
                <button type="button" className="AuthorizeButton" disabled={this.props.disabled} onClick={this.authorize}>
                    <div className="AuthorizeButton__button">
                        <Icon.Shield />
                    </div>

                    <div className="AuthorizeButton__label">
                        {this.props.label}
                    </div>
                </button>
            </>
        )
    }
}
