import React from "react";
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

  export function User(props) {
    props.onBrandChange("Profile");
      return (
          <React.Fragment>
              <Container fluid>
                  <Row>
                      <Col md="8">
                          <Card>
                              <Card.Header>
                                  <Card.Title as="h4">Edit Profile</Card.Title>
                              </Card.Header>
                              <Card.Body>
                                  <Form>
                                      <Row>
                                          <Col className="pr-1" md="5">
                                              <Form.Group>
                                                  <label>Company (disabled)</label>
                                                  <Form.Control
                                                    defaultValue="Train Onboarding"
                                                    disabled
                                                    placeholder="Company"
                                                    type="text"
                                                ></Form.Control>
                                              </Form.Group>
                                          </Col>
                                          <Col className="px-1" md="3">
                                              <Form.Group>
                                                  <label>Username</label>
                                                  <Form.Control
                                                    defaultValue="wafu4975"
                                                    placeholder="Username"
                                                    type="text"
                                                    ></Form.Control>
                                              </Form.Group>
                                          </Col>
                                          <Col className="pl-1" md="4">
                                              <Form.Group>
                                                  <label htmlFor="exampleInputEmail">
                                                      Email Address
                                                  </label>
                                                  <Form.Control
                                                    placeholder="Email"
                                                    type="email"
                                                    ></Form.Control>
                                              </Form.Group>
                                          </Col>
                                      </Row>
                                      <Row>
                                          <Col className="pr-1" md="6">
                                              <Form.Group>
                                                  <label>First Name</label>
                                                  <Form.Control
                                                    defaultValue="Warren"
                                                    placeholder="First Name"
                                                    type="text"
                                                    ></Form.Control>
                                              </Form.Group>
                                          </Col>
                                          <Col className="pl-1" md="6">
                                              <Form.Group>
                                                  <label>Last Name</label>
                                                  <Form.Control
                                                    defaultValue="Fulton"
                                                    placeholder="Last Name"
                                                    type="text"
                                                    ></Form.Control>
                                              </Form.Group>
                                          </Col>
                                      </Row>
                                      <Row>
                                          <Col md="12">
                                              <Form.Group>
                                                  <label>Address</label>
                                                  <Form.Control
                                                    defaultValue="950 28th St."
                                                    placeholder="Home Address"
                                                    type="text"
                                                    ></Form.Control>
                                              </Form.Group>
                                          </Col>
                                      </Row>
                                      <Row>
                                          <Col className="pr-1" md="4">
                                              <Form.Group>
                                                  <label>City</label>
                                                  <Form.Control
                                                    defaultValue="Boulder"
                                                    placeholder="City"
                                                    type="text"
                                                    ></Form.Control>
                                              </Form.Group>
                                          </Col>
                                          <Col className="px-1" md="4">
                                              <Form.Group>
                                                  <label>Country</label>
                                                  <Form.Control
                                                    defaultValue="United States"
                                                    placeholder="Country"
                                                    type="text"
                                                    ></Form.Control>
                                              </Form.Group>
                                          </Col>
                                          <Col className="pl-1" md="4">
                                              <Form.Group>
                                                  <label>Postal Code</label>
                                                  <Form.Control
                                                    placeholder="ZIP Code"
                                                    type="number"
                                                    ></Form.Control>
                                              </Form.Group>
                                          </Col>
                                      </Row>
                                      <Row>
                                          <Col md="12">
                                              <Form.Group>
                                                  <label>About Me</label>
                                                  <Form.Control
                                                    cols="80"
                                                    defaultValue="Senior at the University of Colorado Boulder studying computer science."
                                                    placeholder="Add your description here"
                                                    rows="4"
                                                    as="textarea"
                                                    ></Form.Control>
                                              </Form.Group>
                                          </Col>
                                      </Row>
                                      <Button
                                        className="btn-fill pull-right"
                                        type="submit"
                                        variant="info"
                                        >
                                            Update Profile
                                        </Button>
                                        <div className="clearfix"></div>
                                  </Form>
                              </Card.Body>
                          </Card>
                      </Col>
                      <Col md="4">
                          <Card className="card-user">
                              <div className="card-image">
                                  <img
                                    alt="..."
                                    src={
                                        require("./../Assets/img/boulder.jpg")
                                            .default
                                    }
                                    ></img>
                              </div>
                              <Card.Body>
                                  <div className="author">
                                      <a href="#" onClick={(e) => e.preventDefault()}>
                                          <img
                                            alt="..."
                                            className="avatar border-gray"
                                            src={require("./../Assets/img/warren_image.jpg").default}
                                            ></img>
                                            <h5 className="title">Warren Fulton</h5>
                                      </a>
                                      <p className="description">wafu4975</p>
                                  </div>
                                  <p className="description text-center">
                                      Hello World
                                  </p>
                              </Card.Body>
                              <hr></hr>
                              <div className="button-container mr-auto ml-auto">
                                  <Button
                                    className="btn-simple btn-icon"
                                    href="#"
                                    onClick={(e) => e.preventDefault()}
                                    variant="link"
                                    >
                                        <i className="fab fa-facebook-square"></i>
                                    </Button>
                                    <Button
                                        className="btn-simple btn-icon"
                                        href="#"
                                        onClick={(e) => e.preventDefault()}
                                        variant="link"
                                    >
                                        <i className="fab fa-twitter"></i>
                                    </Button>
                                    <Button
                                        className="btn-simple btn-icon"
                                        href="#"
                                        onClick={(e) => e.preventDefault()}
                                        variant="link"
                                    >
                                        <i className="fab fa-google-plus-square"></i>
                                    </Button>
                              </div>
                          </Card>
                      </Col>
                  </Row>
              </Container>
          </React.Fragment>
      )
  }