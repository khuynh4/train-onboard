import React from 'react';
import { Form,Button, FormControl } from 'react-bootstrap';


export class Signup extends React.Component {
    state = {
        first_name: "",
        last_name: "",
        email: "",
        age: "",
        address: "",
        password: "",
        confirm_pass: ""
    }

    handleSignup = e => {
        e.preventDefault();
        fetch('http://127.0.0.1:5000/api/signup', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                first_name: this.state.first_name,
                last_name: this.state.last_name,
                email: this.state.email,
                age: this.state.age,
                address: this.state.address,
                password: this.state.password,
                confirm_pass: this.state.confirm_pass
            })
        }).then(response => response.json()).then(json => {
            this.props.onSignup(json);
        }).catch(error => {
            console.log(error);
            this.props.onSignupError(error);
        });
    };

    handleFirstNameChange = e => {
        this.setState({
            first_name: e.target.value
        });
    };

    handleLastNameChange = e => {
        this.setState({
            last_name: e.target.value
        });
    };

    handleEmailChange = e => {
        this.setState({
            email: e.target.value
        });
    };

    handleAgeChange = e => {
        this.setState({
            age: e.target.value
        });
    };

    handleAddressChange = e => {
        this.setState({
            address: e.target.value
        });
    };

    handlePasswordChange = e => {
        this.setState({
            password: e.target.value
        });
    };

    handleConfirmPassChange = e => {
        this.setState({
            confirm_pass: e.target.value
        });
    };

    render() {
        return (
            <div className="Login">
                <Form onSubmit={this.handleSubmit}>

                    <Form.Group size="lg" controlId="firstName">
                        <Form.Label>First Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="First Name"
                            value={this.state.first_name}
                            onChange={ this.handleFirstNameChange }
                        ></Form.Control>
                    </Form.Group>

                    <Form.Group size="lg" controlId="lastName">
                        <Form.Label>Last Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Last Name"
                            name="last_name"
                            value={ this.state.last_name }
                            onChange={ this.handlePasswordChange }
                        ></Form.Control>
                    </Form.Group>

                    <Form.Group size="lg" controlId="email">
                        <Form.Label>Email</Form.Label>
                        <Form.Control
                            type="email"
                            placeholder="Email Address"
                            name="email"
                            value={ this.state.email }
                            onChange={ this.handleEmailChange }
                        ></Form.Control>
                        <Form.Text className="text-muted">
                            We'll never share your email with anyone.
                        </Form.Text>
                    </Form.Group>

                    <Form.Group size="lg" controlId="age">
                        <Form.Label>Age</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Age"
                            name="age"
                            value={ this.state.age }
                            onChange={ this.handleAgeChange }
                        ></Form.Control>
                    </Form.Group>

                    <Form.Group size="lg" controlId="address">
                        <Form.Label>Address</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Address"
                            name="address"
                            value={ this.state.address }
                            onChange={ this.handleAddressChange }
                        ></Form.Control>
                    </Form.Group>

                    <Form.Group size="lg" controlId="password">
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Password"
                            name="password"
                            value={ this.state.password }
                            onChange={ this.handlePasswordChange }
                        ></Form.Control>
                    </Form.Group>

                    <Form.Group size="lg" controlId="confirmPassword">
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Confirm Password"
                            name="confirm_pass"
                            value={ this.state.confirm_pass }
                            onChange={ this.handleConfirmPassChange }
                        ></Form.Control>
                    </Form.Group>

                    <Button block size="lg" type="submit" variant="primary" onClick={ this.handleSignup }>
                        Signup
                    </Button>
                </Form>
            </div>
        )
    }
}