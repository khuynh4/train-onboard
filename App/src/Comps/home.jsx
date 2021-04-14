import React from 'react';
import {Jumbotron, Modal, Image, Button, Container, Row, Col} from "react-bootstrap";

import {FiRotateCcw, FiThumbsDown, FiUsers} from "react-icons/fi";
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";

const responsive = {
  desktop: {
    breakpoint: { max: 3000, min: 1024 },
    items: 3,
    slidesToSlide: 3 // optional, default to 1.
  },
  tablet: {
    breakpoint: { max: 1024, min: 464 },
    items: 2,
    slidesToSlide: 2 // optional, default to 1.
  },
  mobile: {
    breakpoint: { max: 464, min: 0 },
    items: 1,
    slidesToSlide: 1 // optional, default to 1.
  }
};


export function Home (props) {
    return (
        <React.Fragment>
            <Container fluid>
            <Jumbotron>
                <div class="text-center">
                    <h1>Train</h1>
                    <h4>
                        We are in the process of designing a great new way to share knowledge within a company. Let's train.
                    </h4>
                    <p>
                        <Button variant="primary">Learn more</Button>
                    </p>
                </div>
            </Jumbotron>
            <Container>
                <h3>
                    Here at trAIn, we are revolutionizing the way training is done in industry.
                </h3>
                <p>
                Current onboarding processes either are unpersonalized, unstructured, or require you to sink repetitive amounts of time and money to perfecting them. When an employee decides to leave, a lot of work is left to be done retraining new hires. Here at trAIn we’re ready to help you do things differently.
                </p>
                <Row>
                    <Col >
                        <img
                            alt="..."
                            className="avatar border-gray"
                            src={require("./../Assets/img/train_logo.jpg").default}
                        ></img>
                    </Col>
                </Row>
                <h3>
                    Problem
                </h3>
                <Row >
                    <Col >
                        <h1><FiRotateCcw/></h1>
                    </Col>
                    <Col>
                        <h1><FiThumbsDown/></h1>
                    </Col>
                    <Col>
                        <h1><FiUsers/></h1>
                    </Col>
                </Row>
                <Row>
                    <Col>
                    Hiring manager have to reinvent the wheel for every new hire.
                    </Col>
                    <Col>
                    Training outcomes are uneven and hard to measure.
                    </Col>
                    <Col>
                    New employees could benefit from past employees knowledge, but it is often not available.
                    </Col>
                </Row>
                <h3>
                    Solution
                </h3>
                <p>
                    We address these problems by helping your managers collaborate to develop training plans for each role. We give you easy customization and creation of training materials through an easy-to-use dashboard, making the creation and management of onboarding plans easy. We help you measure onboarding success by prioritizing goals, progress monitoring, and personalization of training materials to address employees most imminent onboarding problems. We increase collaboration and slash the need for duplicated efforts by allowing you to reuse training templates across similar employees, and similar roles. We keep knowledge within your company by helping employees leave on-the-job tips, resources, and problem-resolution details for future employees to access.
                </p>
                <h3>
                    The Team
                </h3>
                    <Carousel
                        swipeable={false}
                        draggable={false}
                        showDots={true}
                        responsive={responsive}
                        ssr={true} // means to render carousel on server-side.
                        infinite={true}
                        autoPlay={props.deviceType !== "mobile" ? true : false}
                        autoPlaySpeed={1000}
                        keyBoardControl={true}
                        customTransition="all .5"
                        transitionDuration={500}
                        containerClass="carousel-container"
                        removeArrowOnDeviceType={["tablet", "mobile"]}
                        deviceType={props.deviceType}
                        dotListClass="custom-dot-list-style"
                        itemClass="carousel-item-padding-40-px"
                        >
                        <div>
                            <img
                                alt="..."
                                className="avatar border-gray"
                                width="200"
                                src={require("./../Assets/img/andrea.jpg").default}
                            ></img>
                        </div>
                        <div>
                        <img
                                alt="..."
                                className="avatar border-gray"
                                width="200"
                                src={require("./../Assets/img/warren_image.jpg").default}
                            ></img>
                        </div>
                        <div>
                        <img
                                alt="..."
                                className="avatar border-gray"
                                width="200"
                                src={require("./../Assets/img/jake.jpg").default}
                            ></img>
                        </div>
                        <div>
                        <img
                                alt="..."
                                className="avatar border-gray"
                                width="200"
                                src={require("./../Assets/img/kevin.jpg").default}
                            ></img>
                        </div>  
                        <div>
                        <img
                                alt="..."
                                className="avatar border-gray"
                                width="200"
                                src={require("./../Assets/img/michael.jpg").default}
                            ></img>
                        </div>                         
                    </Carousel>;
                <h3>
                    Contact and Demos
                </h3>
                <p>
                Check this page often as we develop more details of this process. We are currently looking for beta-testers of our product!
                To become a beta tester, or just to say hi, drop us a note:
                anch9699@colorado.edu or our LinkedIn’s
                </p>
                
            </Container>
            

                
            </Container>
        </React.Fragment>
    )
}