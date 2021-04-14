import React from 'react';
import { Navbar, Container, Nav, Dropdown, Button } from "react-bootstrap";
import {
    BrowserRouter as Router,
    Switch,
    Route
  } from "react-router-dom";
import { Login } from "../Authentication/login.jsx";
import { Signup } from "../Authentication/signup.jsx";

export function HomeNavbar (props) {
    return (
        <React.Fragment>
            <Navbar bg="light" expand="lg">
                <Container fluid>
                    <div className="d-flex justify-content-center align-items-center ml-2 ml-lg-0">
                        <Navbar.Brand
                            href="/"
                            className="mr-2"
                        >
                            Train
                        </Navbar.Brand>
                    </div>
                    <Navbar.Collapse id="vasic-navbar-nav">
                        <Nav className="nav mr-auto">
                            <Nav.Item>
                                <Nav.Link
                                    className="m-0"
                                    href="#"
                                    onClick={ (e) => e.preventDefault() }
                                >
                                    Pricing
                                </Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link
                                    className="m-0"
                                    href="#"
                                    onClick={ (e) => e.preventDefault() }
                                >
                                    About Us
                                </Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link
                                    className="m-0"
                                    href="#"
                                    onClick={ (e) => e.preventDefault() }
                                >
                                    Contact Us
                                </Nav.Link>
                            </Nav.Item>
                        </Nav>
                        <Nav className="m-0" navbar>
                            <Nav.Item>
                                <Nav.Link
                                    className="m-0"
                                    href="/login"
                                >
                                    <span className="no-icon">Sign In</span>
                                </Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link
                                    className="m-0"
                                    href="/signup"
                                >
                                    <span className="no-icon">Sign Up</span>
                                </Nav.Link>
                            </Nav.Item>
                        </Nav>
                    </Navbar.Collapse>    
                </Container>
            </Navbar>

            <Switch>
                <Route exact path="/"></Route>
                <Route path="/api/login">
                    <Login onLogin={ props.onLogin } onLoginError={ props.onLoginError }/>
                </Route>
                <Route path="/api/signup">
                    <Signup onSignup={ props.onSignup } onSignupError={ props.onSignupError }/>
                </Route>
            </Switch>
        </React.Fragment>
    )
}