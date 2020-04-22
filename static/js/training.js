import React from 'react';
import { client } from './api';


export default class Training extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            // ready: false,
            permissions: 'student',
            ready: true,
            404: false
        }
    }

    // componentDidMount() {
    //     client.get('/api/trainings/' + this.tool)
    //     .then(res => {
    //         console.log(res)
    //         this.setState({
    //             data: res.data,
    //             ready: true,
    //         })
    //     })
    //     .catch(err => {
    //         console.log(err);
    //         this.setState({
    //             404: true,
    //             ready: true,
    //         })
    //     })
    // }

    render() {
        if (!this.state.ready) {
            return (
                <div>
                    Loading your information...
                </div>
            )
        } else if (this.state[404]) {
            window.location.replace("https://http.cat/404");
        } else {
            return (
                <main>
                    <h1>{"<Tool>"} Training</h1>
                    <section className="Checklist">
                        <Checklist permissions={this.state.permissions} />
                    </section>
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
                oldList.reading = e.target.checked;
                oldList.worksheet = !e.target.checked;
                break;
            case 'worksheet':
                oldList.worksheet = e.target.checked;
                oldList.training = !e.target.checked;
                break;
            case 'training':
                oldList.training = e.target.checked;
                oldList.testpiece = !e.target.checked;
                break;
            case 'testpiece':
                oldList.testpiece = e.target.checked;
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
                <h2 className="Checklist__title">Checklist</h2>
                <form>
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

                    <div className="Checklist__text">
                        <label htmlFor="trainer-password">
                            <span>Trainer Password</span>
                            <input type="password" name="" id="trainer-password" />
                        </label>
                        <button type="button" onClick={""}>></button>
                    </div>

                    <div className="Checklist__text">
                        <label htmlFor="trainer-password">
                            <span>Student Password</span>
                            <input type="password" name="" id="trainer-password" />
                        </label>
                        <button type="button" onClick={""}>></button>
                    </div>

                    <div className="Checklist__item">
                        <label>
                            <input className="Checklist__item__checkbox" name={this.props.name} type="checkbox" defaultChecked={false} onChange={""} />
                            <span className="Checklist__item__label">I have read...</span>
                        </label>
                    </div>
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
            <div className="Checklist__item">
                <label>
                    <input className="Checklist__item__checkbox" name={this.props.name} type="checkbox" defaultChecked={false} onChange={this.props.handleCheck} disabled={this.props.disabled} />
                    <span className="Checklist__item__label">{this.props.children}</span>
                </label>
            </div>
        )
    }
}
