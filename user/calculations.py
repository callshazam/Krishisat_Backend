import ee
from datetime import datetime , timedelta
from django.http import JsonResponse

# Initialize GEE (ideally in settings or as a middleware)
ee.Initialize()

def calculate_indices(request):
    geojson_data = request.GET.get('geojson_data')
    start_date = request.GET.get('start_date', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', datetime.now().strftime('%Y-%m-%d'))

    # Convert GeoJSON to GEE geometry
    geojson = ee.Geometry(geojson_data)

    # Load Sentinel-2 data and filter by date and bounds
    collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterDate(start_date, end_date) \
        .filterBounds(geojson)

    # Define calculation of indices
    def calculate_indices(image):
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        rendvi = image.normalizedDifference(['B8', 'B5']).rename('RENDVI')
        ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
        ndmi = image.normalizedDifference(['B8', 'B11']).rename('NDMI')
        ci = image.expression('(B8 / B3) - 1').rename('CI')
        return image.addBands([ndvi, rendvi, ndwi, ndmi, ci])
    
    # Calculate indices and reduce to mean over the area
    image = collection.map(calculate_indices).mean().clip(geojson)
    indices = image.reduceRegion(reducer=ee.Reducer.mean(), geometry=geojson, scale=10)

    # Get the calculated indices
    ndvi = indices.get('NDVI').getInfo()
    rendvi = indices.get('RENDVI').getInfo()
    ndwi = indices.get('NDWI').getInfo()
    ndmi = indices.get('NDMI').getInfo()
    ci = indices.get('CI').getInfo()

    # Return the results as JSON
    return JsonResponse({
        'ndvi': ndvi,
        'rendvi': rendvi,
        'ndwi': ndwi,
        'ndmi': ndmi,
        'ci': ci
    })
