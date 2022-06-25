import axios from 'axios';

async function dashboardData(ranking_method:string, limit:number) {

    let endpoint:string = 'https://api.rarify.tech/data/contracts';
    var params = {
        "include": 'insights',
        "sort": `-insights.${ranking_method}`,
        "page[limit]": limit
    }
    var headers = {
        "Authorization": `Bearer ${process.env.RARIFY_API_KEY}`
    }

    const response = await axios.get(endpoint, {params:params, headers:headers}).then((r:any) => {r.data})
    return response;
}

export {dashboardData};
