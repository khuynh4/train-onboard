import React from 'react';
import { Form,Button } from 'react-bootstrap'
import './../App.css';


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
            <Form onSubmit={ this.handleSubmit }>
                <Form.Group controlId="formFistName">
                    <Form.Label>First Name</Form.Label>
                    <Form.Control 
                        type="text" 
                        placeholder="Enter email"
                        name="first_name"
                        value={ this.state.first_name }
                        onChange={ this.handleFirstNameChange } 
                    />
                    <Form.Text className="text-muted">
                    We'll never share your email with anyone else.
                    </Form.Text>
                </Form.Group>

                <Form.Group controlId="formLastName">
                    <Form.Label>Last Name</Form.Label>
                    <Form.Control 
                        type="text" 
                        placeholder="Last Name"
                        name="last_name"
                        value={ this.state.last_name }
                        onChange={ this.handleLastNameChange } 
                    />
                </Form.Group>

                <Form.Group controlId="formEmail">
                    <Form.Label>Email</Form.Label>
                    <Form.Control 
                        type="email" 
                        placeholder="Enter Emai Address"
                        name="email"
                        value={ this.state.email }
                        onChange={ this.handleEmailChange } 
                    />
                </Form.Group>

                <Form.Group controlId="formAge">
                    <Form.Label>Age</Form.Label>
                    <Form.Control 
                        type="text" 
                        placeholder="Enter Age"
                        name="age"
                        value={ this.state.age }
                        onChange={ this.handleAgeChange } 
                    />
                </Form.Group>

                <Form.Group controlId="formAddress">
                    <Form.Label>Address</Form.Label>
                    <Form.Control 
                        type="text" 
                        placeholder="Address"
                        name="address"
                        value={ this.state.address }
                        onChange={ this.handleAddressChange } 
                    />
                </Form.Group>

                <Form.Group controlId="formPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control 
                        type="password" 
                        placeholder="Password"
                        name="password"
                        value={ this.state.password }
                        onChange={ this.handlePasswordChange } 
                    />
                </Form.Group>

                <Form.Group controlId="formConfrimPass">
                    <Form.Label>Confrim Password</Form.Label>
                    <Form.Control 
                        type="password" 
                        placeholder="Confrim Password"
                        name="confrim_pass"
                        value={ this.state.confirm_pass }
                        onChange={ this.handleConfirmPassChange } 
                    />
                </Form.Group>
                
                <Button 
                    variant="primary" 
                    type="submit"
                    onClick={ this.handleSignup }
                >
                    Submit
                </Button>
            </Form>
            
        )
    }
}