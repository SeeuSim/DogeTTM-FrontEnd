import axios from 'axios';
import { FunctionalComponent, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";

const Ranking: FunctionalComponent = () => {
    const [rankValue, setRankValue] = useState("min_price");
    const [data, setData] = useState({});
    const [loaded, setLoaded] = useState(false)

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

    const changeRank = (e:any) => {
        setRankValue(e.target.value);
    }

    const fetchData = useCallback(() => {
        axios.get(`http://127.0.0.1:8000/top/${rankValue}/`)
        .then((response) => {
            console.log(response);
            setData(response.data);
            setLoaded(true);
        })
    }, []);

    useEffect(() => {
        fetchData
    }, [rankValue])

    const renderTable = (loaded:boolean, value:string) => {
        if (loaded && value == "trending") {
            return renderTrending();
        } else if (loaded) {
            return renderTop();
        }
        return <div><h2>Waiting for Data Type Selection.</h2></div>
    }

    const renderTrending = () => {
        const headers = ["Collection", "Collection Name", "Total Volume", "Percent Change"];

        return (
            <table>
                <thead>
                    <tr>{headers.map((header) => <th class="header">{header}</th>)}</tr>
                </thead>
                <tbody>
                    {}
                </tbody>
            </table>
        );
    }

    const renderTop = () => {
        const values:{[k:string]:string} = {"min_price": "Minimum Sale Value",
                                            "max_price": "Maximum Sale Value",
                                            "volume":    "Total Volume"       };
        const headers = ["Collection", "Collection Name", values[rankValue]];
        return (
            <table>
                <thead>
                    <tr>{headers.map((header) => <th class="header">{header}</th>)}</tr>
                </thead>
                <tbody>
                    {}
                </tbody>
            </table>
        );
    }




    return(
        <div>
            <h1>This is the Ranking Component.</h1>
            <div>
                <select value={rankValue} onChange={changeRank}>
                    <option value="min_price">Min Price</option>
                    <option value="max_price">Max Price</option>
                    <option value="volume">Volume</option>
                    <option value="trending">Trending</option>
                </select>
                <button onClick={fetchData}><h3>See My Data!</h3></button>
            </div>
            {renderTable(loaded, rankValue)}
        </div>
    );
}

export default Ranking;
