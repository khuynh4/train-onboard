import React from "react";
import {
    Badge,
    Button,
    Card,
    Navbar,
    Nav,
    Table,
    Container,
    Row,
    Col,
    Form,
    OverlayTrigger,
    Tooltip,
  } from "react-bootstrap";

  export function TraineeDashboard(props) {

    props.onBrandChange("Dashboard");
    
      return (
        <React.Fragment>
          <Container fludi>
            <Row>
              <Col lg="3" sm="6">
                <Card className="card-stats">
                  <Card.Body>
                    <Row>
                      <Col xs="5">
                        <div className="icon-big text-center icon-warning">
                          <i className="nc-icon nc-chart text-warning"></i>
                        </div>
                      </Col>
                      <Col xs="7">
                        <div className="numbers">
                          <p className="card-category">Number</p>
                          <Card.Title as="h4">150GB</Card.Title>
                        </div>
                      </Col>
                    </Row>
                  </Card.Body>
                  <Card.Footer>
                    <hr></hr>
                    <div className="stats">
                      <i className="fas fa-redo mr-1"></i>
                      Update Now
                    </div>
                  </Card.Footer>
                </Card>
              </Col>
              <Col lg="3" sm="6">
                <Card className="card-stats">
                  <Card.Body>
                    <Row>
                      <Col xs="5">
                        <div className="icon-big text-center icon-warning">
                          <i className="nc-icon nc-light-3 text-success"></i>
                        </div>
                      </Col>
                      <Col xs="7">
                        <div className="numbers">
                          <p className="card-category">Revenue</p>
                          <Card.Title as="h4">$1,345</Card.Title>
                        </div>
                      </Col>
                    </Row>
                  </Card.Body>
                  <Card.Footer>
                    <hr></hr>
                    <div className="stats">
                      <i className="far fa-calendar-alt mr-1"></i>
                      Last Day
                    </div>
                  </Card.Footer>
                </Card>
              </Col>
              <Col lg="3" sm="6">
                <Card className="card-stats">
                  <Card.Body>
                    <Row>
                      <Col xs="5">
                        <div className="icon-big text-center icon-warning">
                          <i className="nc-icon nc-vector text-danger"></i>
                        </div>
                      </Col>
                      <Col xs="7">
                        <div className="numbers">
                          <p className="card-category">Errors</p>
                          <Card.Title as="h4">23</Card.Title>
                        </div>
                      </Col>
                    </Row>
                  </Card.Body>
                  <Card.Footer>
                    <hr></hr>
                    <div className="stats">
                      <i className="far fa-clock-o mr-1"></i>
                      In The Last hour
                    </div>
                  </Card.Footer>
                </Card>
              </Col>
              <Col lg="3" sm="6">
                <Card className="card-stats">
                  <Card.Body>
                    <Row>
                      <Col xs="5">
                        <div className="icon-big text-center icon-warning">
                          <i className="nc-icon nc-favorite-28 text-primary"></i>
                        </div>
                      </Col>
                      <Col xs="7">
                        <div className="numbers">
                          <p className="card-category">Followers</p>
                          <Card.Title as="h4">+45k</Card.Title>
                        </div>
                      </Col>
                    </Row>
                  </Card.Body>
                  <Card.Footer>
                    <hr></hr>
                    <div className="stats">
                      <i className="fas fa-redo mr-1"></i>
                      Update Now
                    </div>
                  </Card.Footer>
                </Card>
              </Col>
            </Row>
            <Row>
              <Col md="8">
                <Card>
                  <Card.Header>
                    <Card.Title as="h4">Users Behavior</Card.Title>
                    <p className="card-category">24 Hours Performance</p>
                  </Card.Header>
                  <Card.Body></Card.Body>
                  <Card.Footer>
                    <hr></hr>
                    <div className="stats">
                      <i className="fas fa-history"></i>
                      Updated 3 minutes ago
                    </div>
                  </Card.Footer>
                </Card>
              </Col>
              <Col md="h4">
                <Card>
                  <Card.Header>
                    <Card.Title as="h4">Email Statistics</Card.Title>
                    <p className="card-category">Last Capmaign Performance</p>
                  </Card.Header>
                  <Card.Body>

                  </Card.Body>
                </Card>
              </Col>
            </Row>
            <Row>
              <Col md="6">
                <Card>
                  <Card.Header>
                    <Card.Title as="h4">2017 Sales</Card.Title>
                    <p className="card-category">All products including taxes</p>
                  </Card.Header>
                  <Card.Body>

                  </Card.Body>
                  <Card.Footer>
                    <hr></hr>
                    <div className="stats">
                      <i className="fas fa-check"></i>
                      Data information certified
                    </div>
                  </Card.Footer>
                </Card>
              </Col>
            </Row>
          </Container>
        </React.Fragment>
      )
  }
