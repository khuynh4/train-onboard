import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route
  } from "react-router-dom";
import { Navbar,Nav,Form,FormControl,Button } from 'react-bootstrap'
import { Login } from './Authentication/login';
import { Signup } from './Authentication/signup';
import LoggedInDisplay from './loggedInDisplay';
import 'bootstrap/dist/css/bootstrap.css';

export function Header(props) {

        return (
            <div className="row">
                <div className="col-md-12">
                    <Router>
                        <Navbar bg="dark" variant="dark" expand="lg" sticky="top">
                            <Navbar.Brand href="/">Train</Navbar.Brand>
                                <Nav className="mr-auto">
                                    <LoggedInDisplay isLoggedIn={ props.isLoggedIn } name={ props.name } onLogout={ props.onLogout }key="loggedInDisplay"/>
                                </Nav>
                                <Form inline>
                                <FormControl type="text" placeholder="Search" className="mr-sm-2" />
                                <Button variant="outline-success" style={{color: "#87ceeb", borderColor: "#87ceeb"}}>Search</Button>
                                </Form>
                        </Navbar>
                        <br />
                        <Switch>
                            <Route exact path="/api/login">
                                <Login onLogin={ props.onLogin } onLoginError={ props.onLoginError }/>
                            </Route>
                            <Route path="/api/signup">
                                <Signup onSignup={ props.onSignup } onSignupError={ props.onSignupError }/>
                            </Route>
                        </Switch>
                    </Router>
                </div>
            </div>
        )

        }
    