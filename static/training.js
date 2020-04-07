import React from 'react';
import { client } from './api';


export default class Training extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
            ready: false,
        }
    }

    componentDidMount() {
        client.get('/api/trainings/' + this.tool)
        .then(res => {
            console.log(res)
            this.setState({
                data: res.data,
                ready: true,
            })
        })
        .catch(err => {
            console.log(err);
            this.setState({
                404: true,
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
                <div>
                    
                </div>
            )
        }
    }
}
