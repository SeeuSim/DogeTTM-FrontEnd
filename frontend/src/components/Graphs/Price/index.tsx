import axios from 'axios';
import { CanvasJSChart } from 'canvasjs-react-charts';
import { FunctionalComponent, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";
import * as URLCONFIG from "../../../../URLCONF.json";

const baseURL = URLCONFIG.endpoint;

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
    const [loaded, setLoaded] = useState<Boolean>(false);

    const fetchPriceDP = useCallback(() => {
        axios.get<PDPackage>(`${baseURL}/history/price/${address}/${time}`)
        .then((response) => {
            console.log(response);
            setPriceDP(response.data['data']);
            setLoaded(true);
        })
    }, []);

    useEffect(() => {
        fetchPriceDP()
        renderGraph()
    }, [priceDP]);

    const renderGraph = () => {
        if (typeof priceDP != "undefined") {
            console.log("rendering");
            const options = {
                animationEnabled: true,
                title:{
                    text: `Price History for ${time}`
                },
                axisY : {
                    title: "Price in ETH"
                },
                toolTip: {
                    shared: true
                },
                data: [{
                    type: "spline",
                    name: "Average Price",
                    showInLegend: true,
                    dataPoints: priceDP.map((row) => {
                        return {y:parseFloat(row['avg_price']) * Math.pow(10, -18), label:row['time']};
                    })
                }, {
                    type: "spline",
                    name: "Minimum Price",
                    showInLegend: true,
                    dataPoints: priceDP.map((row) => {
                        return {y:parseFloat(row['min_price']) * Math.pow(10, -18), label:row['time']};
                    })
                }, {
                    type: "spline",
                    name: "Maximum Price",
                    showInLegend: true,
                    dataPoints: priceDP.map((row) => {
                        return {y:parseFloat(row['max_price']) * Math.pow(10, -18), label:row['time']};
                    })
                }]
            }
            return (
                <div><CanvasJSChart options={options} /></div>
            );

        }
        return <div><h1>Loading</h1></div>;
    };
    return renderGraph();
};

export default PriceGraph;

