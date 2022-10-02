import React from "react";
import {
    NotificationContainer,
    NotificationManager
} from "react-notifications";
import "react-notifications/lib/notifications.css";
import { connect } from "react-redux";

class Notifications extends React.Component {
    createNotification = (type) => {
        if (this.props.notification?.message) {
            setTimeout(() => {
                switch (this.props.notification?.type) {
                    case "info":
                        NotificationManager.info(
                            this.props.notification?.message,
                            "Info",
                            1000
                        );
                        break;
                    case "success":
                        NotificationManager.success(
                            this.props.notification.message,
                            "Success",
                            1000
                        );
                        break;
                    case "warning":
                        NotificationManager.warning(
                            this.props.notification.message,
                            "Warning",
                            1000
                        );
                        break;
                    case "error":
                        NotificationManager.error(
                            this.props.notification.message,
                            "Error",
                            1000
                        );
                        break;
                    default:
                        NotificationManager.error(
                            this.props.notification.message,
                            "Error",
                            1000
                        );
                }
            }, 0);
        }
    };

    render() {
        return (
            <div>
                <NotificationContainer />
                {this.createNotification()}
            </div>
        );
    }
}

const mapStateToProps = (state, ownProps) => {
    return {
        // notification: state.common.notification,
    };
};

export default connect(mapStateToProps)(Notifications);
