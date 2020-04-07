import React from 'react';
import { client } from './api';


export default class Training extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            // ready: false,
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
                    <section>
                        <Checklist />
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

        }
    }
    handleCheck(e) {
        console.log(e.target.checked)
    }

    render() {
        return (
            <div>
                <h2>Checklist</h2>
                <form>
                    <div>
                        <label>
                            Completed <a href="#">Readings</a>
                            <input type="checkbox" defaultChecked={false} onChange={this.handleCheck} />
                        </label>
                    </div>

                    <div>
                        <label>
                            Completed <a href="#">Worksheet</a>
                            <input type="checkbox" defaultChecked={false} onChange={this.handleCheck} />
                        </label>
                    </div>

                    <div>
                        <label>
                            Completed Training
                            <input type="checkbox" defaultChecked={false} onChange={this.handleCheck} />
                        </label>
                    </div>

                    <div>
                        <label>
                            Completed Test Piece
                            <input type="checkbox" defaultChecked={false} onChange={this.handleCheck} />
                        </label>
                    </div>
                </form>
            </div>
        )
    }
}
