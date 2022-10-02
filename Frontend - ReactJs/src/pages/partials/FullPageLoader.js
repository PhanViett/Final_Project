import React, { Component } from "react";
import { Oval } from "react-loader-spinner";
import { connect } from "react-redux";

class FullPageLoader extends Component {
    state = {};

    render() {
        const { loading } = this.props;

        if (!loading) return null;

        return (
            <div id="common-loading">
                <div className="loader">
                    <Oval arialLabel="loading-indicator" color="#007bff" height={80} />
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state) => ({ 
    // loading: state.common.loading 
});

export default connect(mapStateToProps)(FullPageLoader);
