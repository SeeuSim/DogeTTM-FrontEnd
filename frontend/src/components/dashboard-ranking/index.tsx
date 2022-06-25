import { Component, FunctionalComponent, h , render} from 'preact';
import { useCallback, useEffect, useState } from 'preact/hooks';
import { Link } from 'preact-router/match';
import axios, { AxiosResponse } from 'axios';
import style from './style.css';

export default class Dashboard_Ranking extends Component{
    state = {
        value:"min_price",
        limit:5,
        dashboard_data:{"data":["loading"], 'included':["loading"]}
    };

    trendingData = {
        'data': [{'attributes':{'name': "", 'address':""}}],
        'included':[{'attributes':{
            'payment_asset':{'code':"", 'image_url':""},
            'volume_change':"",
            'volume_change_percent':0
        }}]
    };
    topRanking = {
        'data': [{'attributes': {'address': '','name': ''}}],
        'included': [{'attributes': {
        'max_price': '',
        'min_price': '',
        'payment_asset': {'code': '',
                          'image_url': ''},
        'volume': ''}}]
    }

    onChange = (e:any) => {
        this.setState({ value: e.target.value });
    };

    fetchData = useCallback(() => {
        axios({
            "method": "GET",
            "url": this.state.value != "trending"
                ? "https://api.rarify.tech/data/contracts"
                : "",
            "headers": {
                "Authorization": `Bearer ${process.env.RARIFY_API_KEY}`
            },
            "params": this.state.value != "trending"
                ? {
                    "include": 'insights',
                    "sort": `-insights.${this.state.value}`,
                    "page[limit]": this.state.limit
                }
                : {
                    'insights_trends.period': "7d",
                    'include': 'insights_trends',
                    'sort': '-insights_trends.volume_change_percent',
                    'page[limit]': this.state.limit
                }
        })
        .then((response:AxiosResponse) => {
            this.setState({dashboard_data:response.data});
            this.state.value == 'trending'
                ? this.trendingData = response.data
                : this.topRanking = response.data;
        })
        .catch((error) => {
            this.setState({dashboard_data:{"errors":error}})
        })
    }, [])

    renderTrending() {
        let headings:any[] = ["Collection", "Collection Name", "Total Volume", "Percent Change"];
        let tokens:any[] = this.state.dashboard_data['data'];
        let data:any[] = this.state.dashboard_data['included'];
        return (
            <table class="mainTable">
                <tr class="tableTitle">
                    {headings.map((header:string) => {
                        return (<th class="tableHeader">`${header}`</th>)
                    })}
                </tr>
                {}
            </table>
        )
    }

    render(props:any, state:any) {
        return (
            <div class="Dashboard_Ranking">
                <select value={state.value} onChange={this.onChange}>
                    <option value="min_price">Minimum Price</option>
                    <option value="max_price">Maximum Price</option>
                    <option value="volume">Volume</option>
                    <option value="trending">Trending</option>
                </select>
                <div>

                </div>
            </div>
        )
    }
}

