import React, { Component } from "react";
import { DayPilot, DayPilotCalendar, DayPilotNavigator } from "daypilot-pro-react";

const styles = {
    wrap: {
        display: "flex"
    },
    left: {
        marginRight: "10px"
    },
    main: {
        flexGrow: "1"
    }
};

export class Calendar extends Component {
    constructor(props) {
        props.onBrandChange("Calendar");
        super(props);
        this.state = {
            viewType: "Week",
            durationBarVisible: false,
            timeRangeSelectHandling: "Enabled",
            onTimeRangeSelected: args => {
                let dp = this.calendar;
                DayPilot.Modal.prompt("Create a new event:", "Event 1").then(function(modal) {
                    dp.clearSelection();
                    if (!modal.result) { return; }
                    dp.events.add(new DayPilot.Event({
                        start: args.start,
                        end: args.end,
                        id: DayPilot.guid(),
                        text: modal.result
                    }));
                });
            },
            eventDeleteHandling: "Update",
            onEventClick: args => {
                let dp = this.calendar;
                DayPilot.Modal.prompt("Update event text:", args.e.text()).then(function(modal){
                    if (!modal.result) { return; }
                    args.e.data.text = modal.result;
                    dp.events.update(args.e);
                });
            },
        };
    }

    componentDidMount() {
        this.setState({
            startDate: "2021-04-11",
            events: [
                {
                    id: 1,
                    text: "Event 1",
                    start: "2021-04-11T10:30:00",
                    end: "2021-04-11T13:00:00"
                }, 
                {
                    id: 3,
                    text: "Event 3",
                    start:"2021-04-12T12:00:00",
                    end: "2021-04-12T15:00:00",
                    backColor: "#cc4125"
                }
            ]
        });
    }

    render() {
        var {...config} = this.state;

        return (
            <div style={ styles.wrap }>
                <div style={ styles.left }>
                    <DayPilotNavigator
                        selectMode={"week"}
                        showMonths={3}
                        skipMonths={3}
                        onTimeRangeSelected={ args => {
                            this.setState({
                                startDate: args.day
                            });
                        }}
                    />
                </div>
                <div style={styles.main}>
                    <DayPilotCalendar
                        {...config}
                        ref={component => {
                            this.calendar = component && component.control;
                        }}
                    />
                </div>
            </div>
        );
    }
}