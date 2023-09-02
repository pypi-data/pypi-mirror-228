def normalize_data(data):
    return (data - data.min()) / (data.max() - data.min())
