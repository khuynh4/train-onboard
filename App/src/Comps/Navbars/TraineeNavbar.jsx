import React, { useEffect, useState } from "react";
import { Navbar, Container, Nav, Dropdown, Button } from "react-bootstrap";
import { BsCircleSquare } from "react-icons/bs"
import { BiSearchAlt } from "react-icons/bi"
import { useLocation } from 'react-router-dom';

export function TraineeNavbar (props) {
    const { onLogout, brand } = props;

    return (
        <Navbar bg="light" expand="lg">
            <Container fluid>
                <div className="d-flex justify-content-center align-items-center ml-2 ml-lg-0">
                    <Navbar.Brand
                        href="/"
                        onClick={(e) => e.preventDefault()}
                        className="mr-2"
                    >
                        { brand }
                    </Navbar.Brand>
                </div>
                <Navbar.Collapse id="vasic-navbar-nav">
                    <Nav className="nav mr-auto">
                        <Dropdown as={Nav.Item}>
                            <Dropdown.Toggle
                                as={Nav.Link}
                                data-toggle="dropdown"
                                id="dropdown-67443507"
                                variant="default"
                                className="m=0"
                            >
                                <BsCircleSquare />
                            </Dropdown.Toggle>
                            <Dropdown.Menu>
                                <Dropdown.Item
                                    href="#"
                                    onClick ={ (e) => e.preventDefault() }
                                >
                                    Notification 1
                                </Dropdown.Item>
                                <Dropdown.Item
                                    href="#"
                                    onClick ={ (e) => e.preventDefault() }
                                >
                                    Notification 2
                                </Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                    </Nav>
                    <Nav className="m-0" navbar>
                        <Nav.Item>
                            <Nav.Link
                                className="m-0"
                                href="#"
                                onClick={ (e) => e.preventDefault() }
                            >
                                <span className="no-icon">Account</span>
                            </Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link
                                className="m-0"
                                href="/"
                                onClick={ onLogout }
                            >
                                <span className="no-icon">Logout</span>
                            </Nav.Link>
                        </Nav.Item>
                    </Nav>
                </Navbar.Collapse>
                    
            </Container>
        </Navbar>
    )
}