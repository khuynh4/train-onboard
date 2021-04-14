import React, { useEffect, useState } from 'react';
import { Container } from 'react-bootstrap';
import { TraineeSidebar } from "./../Comps/Sidebars/TraineeSidebar.jsx";
import { TraineeNavbar } from "./../Comps/Navbars/TraineeNavbar.jsx";
import { TraineeDashboard } from "./../Views/TraineeDashboard.jsx";
import { User } from "./../Views/UserProfile.jsx";
import { Calendar } from "./../Views/Calendar.jsx";
import {
    BrowserRouter as Router,
    Switch,
    Route
  } from "react-router-dom";

export function TraineeLayout (props) {
    const { name, onLogout} = props;

    const [brand, setBrand] = useState("");

    const onBrandChange = (brand) => {
        setBrand(brand);
    }

    useEffect(() => {
        console.log("Updated Brand");
    }, [brand]);

    return (
        <React.Fragment>
            <div className="wrapper">
                <TraineeSidebar name={ name }/>
                <div className="main-panel">
                    <TraineeNavbar onLogout={ onLogout } brand={ brand }/>  
                    <div className="content">
                        <Switch>
                            <Route path="/user/dashboard">
                                <TraineeDashboard onBrandChange={ onBrandChange }/>
                            </Route>
                            <Route path="/user/user-profile">
                                <User onBrandChange={ onBrandChange }/>
                            </Route>
                            <Route path="/user/calendar">
                                <Calendar onBrandChange={ onBrandChange }/>
                            </Route>
                        </Switch>
                    </div>
                </div>
            </div>
        </React.Fragment>
    )
    
}