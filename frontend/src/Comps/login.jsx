import React from 'react';
import { Form,Button } from 'react-bootstrap';

export class Login extends React.Component {
    state = {
        email: "",
        password: ""
    };

    handleLogin = e => {
        e.preventDefault();
        fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://localhost:3000'
            },
            body: JSON.stringify({
                email: this.state.email,
                password: this.state.password
            })
        }).then(response => response.json()).then(json => {
            this.props.onLogin(json);
        }).catch(error => {
            this.props.onLoginError(error);
        });
    };

    handleEmailChange = e => {
        this.setState({
            email: e.target.value
        });
    };

    handlePasswordChange = e => {
        this.setState({
            password: e.target.value
        });
    };

    render() {
        return (
            <Form onSubmit={ this.handleSubmit }>
                <Form.Group controlId="formBasicEmail">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control 
                        type="email" 
                        placeholder="Enter email"
                        name="email"
                        value={this.state.email}
                        onChange={this.handleEmailChange} 
                    />
                    <Form.Text className="text-muted">
                    We'll never share your email with anyone else.
                    </Form.Text>
                </Form.Group>

                <Form.Group controlId="formBasicPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control 
                        type="password" 
                        placeholder="Password"
                        value={this.state.password}
                        onChange={this.handlePasswordChange}
                    />
                </Form.Group>

                <Button 
                    variant="primary" 
                    type="submit"
                    onClick={ this.handleLogin }
                >
                    Submit
                </Button>
            </Form>
        );
    }
}