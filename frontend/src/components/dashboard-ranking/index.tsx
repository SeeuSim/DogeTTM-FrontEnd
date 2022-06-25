import axios, { AxiosResponse } from 'axios';
import { FunctionalComponent, h } from 'preact';
import { useCallback } from 'preact/hooks';

const Dashboard_Ranking:FunctionalComponent = () => {
    var state = {
        value:"min_price",
        limit:5,
        dashboard_data:{"data":["loading"], 'included':["loading"], 'errors': []}
    };

    var trendingData = {
        'data': [{'attributes':{'name': ""}, "id":""}],
        'included':[{'attributes':{
            'payment_asset':{'code':"", 'image_url':""},
            'volume_change':"",
            'volume_change_percent':0
        }}]
    };
    var topRanking = {
        'data': [{'attributes': {'name': ''}}],
        'id':"",
        'included': [{'attributes': {
        'max_price': '',
        'min_price': '',
        'payment_asset': {'code': '',
                          'image_url': ''},
        'volume': ''}}]
    }

    const onChange = (e:any) => {
        state.value = e.target.value;
    };

    var fetchData = useCallback(() => {
        axios({
            "method": "GET",
            "url": state.value != "trending"
                ? "https://api.rarify.tech/data/contracts"
                : "",
            "headers": {
                "Authorization": `Bearer ${process.env.RARIFY_API_KEY}`
            },
            "params": state.value != "trending"
                ? {
                    "include": 'insights',
                    "sort": `-insights.${state.value}`,
                    "page[limit]": state.limit
                }
                : {
                    'insights_trends.period': "7d",
                    'include': 'insights_trends',
                    'sort': '-insights_trends.volume_change_percent',
                    'page[limit]': state.limit
                }
        })
        .then((response:AxiosResponse) => {
            state.dashboard_data = response.data;
            state.value == 'trending'
                ? trendingData = response.data
                : topRanking = response.data;
        })
        .catch((error) => {
            state.dashboard_data['errors'] = error;
        })
    }, [state.value])

    var fetchArtWork = (address:string) => {
        const collection = `https://api.rarify.tech/data/contracts/${address}`
        var nums = 0
        axios.get(collection, {headers: {"Authorization": `Bearer ${process.env.RARIFY_API_KEY}`}})
            .then((response) => response.data)
            .catch((error) => {
                return {'data':{"attributes":{"tokens":0}}};
            })
            .then((data) => {
                nums = data['data']['attributes']['tokens'];
            });

        let hashed_id = nums.toString(16)
        if (hashed_id.length % 2 == 0) {
            hashed_id = hashed_id.substring(2);
        } else {
            hashed_id = hashed_id.replace("x", "");
        }

        const url = `https://api.rarify.tech/data/tokens/${address}:${hashed_id}`;
        var img = "";
        axios.get(url, {headers: {"Authorization": `Bearer ${process.env.RARIFY_API_KEY}`}})
            .then((response) => response.data)
            .catch((error) => {
                return {"data":{"attributes":{"image_url":""}}};
            })
            .then((data) => {
                img = data['data']['attributes']['image_url'];
            });
        return img
    }

    var renderTrending = () => {
        let headings:any[] = ["Collection", "Collection Name", "Total Volume", "Percent Change"];
        let tokens:any[] = trendingData['data'];
        let data:any[] = trendingData['included'];
        return (
            <table class="mainTable">
                <tr class="tableTitle">
                    {headings.map((header:string) => {
                        return (<th class="tableHeader">`${header}`</th>)
                    })}
                </tr>
                {tokens.map((token, index) => {
                    const dataCell = data[index];
                    const address = token['id'];
                    const coin_image:string = dataCell['attributes']['payment_asset']['image_url'];
                    return (
                        <tr class="tokenRow">
                            <td>
                                <img src = {fetchArtWork(address)}></img>
                            </td>
                            <td>`{token['attributes']['name']}`</td>
                            <td>
                                `{dataCell['attributes']['volume_change']} {dataCell['attributes']['payment_asset']['code']}`
                                <img src={coin_image}></img>
                            </td>
                            <td>
                                `{dataCell['attributes']['volume_change_percent']}%`
                            </td>
                        </tr>)
                })}
            </table>
        )
    }

    var renderTop = ()=>{
        const values:{[k:string]:string[]} = {
            "min_value": ["Minimum Sale Value", "min_price"],
            "max_value": ["Maximum Sale Value", "max_price"],
            "volume": ["Total Volume", "volume"]
        }

        let headings:any[] = ["Collection", "Collection Name", values[state.value][0]];
        let tokens:any[] = topRanking['data'];
        let data:any[] = topRanking['included'];

        return (
            <table class="mainTable">
                <tr class="tableTitle">
                    {headings.map((header:string) => {
                        return (<th class="tableHeader">`${header}`</th>)
                    })}
                </tr>
                {tokens.map((token, index) => {
                    const dataCell = data[index];
                    const address = token['id'];
                    const coin_image:string = dataCell['attributes']['payment_asset']['image_url'];
                    return (
                        <tr class="tokenRow">
                            <td>
                                <img src = {fetchArtWork(address)}></img>
                            </td>
                            <td>`{token['attributes']['name']}`</td>
                            <td>
                                `{dataCell['attributes'][values[state.value][1]]} {dataCell['attributes']['payment_asset']['code']}`
                                <img src={coin_image}></img>
                            </td>
                        </tr>)
                })}
            </table>
        )
    }

    var renderTable = (props:any) => {
        const isTrending = props.value == "trending";
        if (isTrending) {
            return renderTrending()
        } else {
            return renderTop()
        }
    }


    return (
        <div class="Dashboard_Ranking">
            <select value={state.value} onChange={onChange}>
                <option value="min_price">Minimum Price</option>
                <option value="max_price">Maximum Price</option>
                <option value="volume">Volume</option>
                <option value="trending">Trending</option>
            </select>
            <div>
                {renderTable(state.value)}
            </div>
        </div>
        )

}

export default Dashboard_Ranking;
