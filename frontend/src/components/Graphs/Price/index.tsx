import axios from 'axios';
import { FunctionalComponent, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";
import * as URLCONFIG from "../../../../URLCONF.json";

const baseURL = URLCONFIG.BACKEND;

interface PriceGraph{
    address:string,
    time:string
}

interface PriceData{
    'avg_price': string,
    'max_price': string,
    'min_price': string,
    'time': string,
    'trades': string,
    'unique_buyers': string,
    'volume': string
}

interface PDPackage{
    "data": PriceData[]
}

const PriceGraph:FunctionalComponent<PriceGraph> = (props:PriceGraph) => {
    const {address, time} = props;
    const [priceDP, setPriceDP] = useState<PriceData[]>();

    const fetchPriceDP = useCallback(() => {
        axios.get<PDPackage>(`${baseURL}/history/price/${address}/${time}`)
        .then((response) => {
            console.log(response);
            setPriceDP(response.data['data']);
        })
    }, []);

    useEffect(() => {
        fetchPriceDP();
    }, [priceDP]);

    return <div></div>;
};

export default PriceGraph;

