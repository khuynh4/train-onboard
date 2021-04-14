import React from 'react';
import {
    Badge,
    Button,
    Card,
    Form,
    Navbar,
    Nav,
    Container,
    Row,
    Col,
  } from "react-bootstrap";
  import { Link } from 'react-router-dom';

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
            <div className="Login">
                <Form onSubmit={ this.handleSubmit }>
                    <Form.Group size="lg" controlId="email">
                        <Form.Label>Email</Form.Label>
                        <Form.Control
                            autoFocus
                            type="email"
                            placeholder="Email"
                            value={this.state.email}
                            onChange={this.handleEmailChange}
                        ></Form.Control>
                        <Form.Group size="lg" controlId="password">
                            <Form.Label>Password</Form.Label>
                            <Form.Control
                                type="password"
                                value={this.state.password}
                                placeholder="Password"
                                onChange={this.handlePasswordChange}
                            ></Form.Control>
                        </Form.Group>
                        <Button block size="lg" type="submit" variant="primary" onClick={this.handleLogin}>
                            <Link to="/user/dashboard" style={{color: "white"}}>Login</Link>
                        </Button>
                    </Form.Group>
                </Form>
            </div>
        );
    }
}