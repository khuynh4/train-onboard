import React from 'react';
import { Nav } from 'react-bootstrap';

function LoggedInDisplay(props) {
    const isLoggedIn = props.isLoggedIn;
    const name = props.name;
    if (isLoggedIn) {
        return ([
            <Nav key="loggedOutNav">
                <div className="row" key="loggedOutDisplay">
                    <Nav.Link eventKey="disabled" disabled style={{marginLeft: 20, color: "#87ceeb"}} key="name">{ name }</Nav.Link>,
                    <Nav.Link href="/api/logout" style={{marginLeft: 20, color: "#87ceeb"}} onClick={ props.onLogout } key="logout">Logout</Nav.Link>
                </div>
            </Nav>
        ]);
    }
    return ([
        <Nav key="loggedInNav">
            <div className="row" key="loggedInDisplay">
                <Nav.Link href="/api/login" style={{marginLeft: 20, color: "#87ceeb"}} key="login">Login</Nav.Link>,
                <Nav.Link href="/api/signup" style={{marginLeft: 20, color: "#87ceeb"}} key="signup">Signup</Nav.Link>
            </div>
        </Nav>
    ]);
};

export default LoggedInDisplay;