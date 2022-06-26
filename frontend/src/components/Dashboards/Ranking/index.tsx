import axios from 'axios';
import { FunctionalComponent, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";
import style from "./style.css";
import * as URLCONFIG from "../../../../URLCONF.json";

const baseURL = URLCONFIG.endpoint;

interface TrendingData {
    "imgurl":string,
    "address":string,
    "name":string,
    "tokens":string,
    "unique_owners":string,
    "volume_change":string,
    "percent_change":string,
}

interface TopRankData {
    "imgurl":string,
    "address":string,
    "name":string,
    "tokens":string,
    "min_price":string,
    "max_price":string,
    "volume":string,
    "avg_price":string,
}

interface RankResponse {
    "data":TopRankData[]
}

interface TrendResponse {
    "data": TrendingData[]
}

const Ranking: FunctionalComponent = () => {
    const [rankValue, setRankValue] = useState("min_price");
    const [rankData, setRankData] = useState<RankResponse>();
    const [trendData, setTrendData] = useState<TrendResponse>();
    const [loaded, setLoaded] = useState(false)
    const [trendTimeValue, setTimeValue] = useState('7d');

    const changeRank = (e:any) => {
        setRankValue(e.target.value);
        console.log(rankValue)
    };

    const changeTime = (e:any) => {
        setTimeValue(e.target.value);
    }

    const fetchRankData = useCallback(() => {
        axios.get<RankResponse>(`${baseURL}/toprank/${rankValue}`)
        .then((response) => {
            console.log(response);
            setRankData(response.data);
            setLoaded(true);
        })
    }, [rankValue!="trending"]);

    const fetchTrendData = useCallback(() => {
        axios.get<TrendResponse>(`${baseURL}/toptrend/${trendTimeValue}`)
        .then((response) => {
            console.log(response);
            setTrendData(response.data);
            setLoaded(true);
        })
    }, [rankValue=="trending"])

    const fetchData = () => {
        if (rankValue == "trending") {
            fetchTrendData();
        }
        fetchRankData()
    }
    useEffect(() => {
        fetchData
    }, [])

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
        const values:TrendResponse|undefined = trendData;
        var rows = [1].map((i) => <tr>{headers.map((header) => <td>Data Loading</td>)}</tr>)

        if (typeof values != 'undefined') {
            const raw = values['data'];
            rows = raw.map<h.JSX.Element>((row) => (
                <tr>
                    <td><img class={style.TableImg} src={row['imgurl']}></img></td>
                    <td>
                        <a href={`/collections/${row['address']}`}>
                            {row['name']}
                        </a>
                    </td>
                    <td>{row['volume_change']}</td>
                    <td>{row['percent_change']}</td>
                </tr>
            ))
        }

        return (
            <table>
                <thead>
                    <tr>{headers.map((header) => <th class="header">{header}</th>)}</tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        );
    }

    const renderTop = () => {
        const values:{[k:string]:string} = {"min_price": "Minimum Sale Value",
                                            "max_price": "Maximum Sale Value",
                                            "volume":    "Total Volume"       };
        const headers = ["Collection", "Collection Name", values[rankValue]];
        const raw:RankResponse|undefined = rankData;
        var rows = [1].map((i) => <tr>{headers.map((header) => <td>Data Loading</td>)}</tr>)


        if (typeof raw != "undefined") {
            const rawRows = raw['data']
            rows = rawRows.map<h.JSX.Element>((row) => (
                <tr>
                    <td><img class={style.TableImg} src={row['imgurl']}></img></td>
                    <td>
                        <a href={`/collections/${row['address']}`}>
                            {row['name']}
                        </a>
                    </td>
                    <td>{row[rankValue=="min_price"
                                ? "min_price"
                                : rankValue == "max_price"
                                ? "max_price"
                                : "volume"]}</td>
                </tr>
            ))
        }
        return (
            <table>
                <thead>
                    <tr>{headers.map((header) => <th class="header">{header}</th>)}</tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        );
    }

    return(
        <div>
            <div>
                <select value={rankValue} onChange={changeRank}>
                    <option value="min_price">Min Price</option>
                    <option value="max_price">Max Price</option>
                    <option value="volume">Volume</option>
                    <option value="trending">Trending</option>
                </select>
                {rankValue=="trending"
                    ?   <select value={trendTimeValue} onChange={changeTime}>
                            <option value="24h">24h</option>
                            <option value="3d">3d</option>
                            <option value="7d">7d</option>
                            <option value="30d">30d</option>
                            <option value="90d">90d</option>
                        </select>
                    : null}
                <button onClick={fetchData}><h3>See My Data!</h3></button>
            </div>
            {renderTable(loaded, rankValue)}
        </div>
    );
}

export default Ranking;
