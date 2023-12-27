from bollards_api.models import Bollard



def get_neighbours_by_number(current_bollard):
    """
    Get the position, number and name of the closest bollards 
    (1no before, same no and 1no after)

    @return an array of all neighbouring bollards
    """
    current_number = current_bollard.b_number

    neighbours = Bollard.query.filter(
        Bollard.b_number > current_number - 20, 
        Bollard.b_number < current_number + 20 
        ).all()
    neighbours.remove(current_bollard)

    res = []
    for neighbour in neighbours:
        res.append({
            'id': neighbour.id,
            'b_number': neighbour.b_number,
            'b_letter': neighbour.b_letter,
            'b_type': neighbour.b_type,
            'b_lat': str(neighbour.b_lat),
            'b_lng': str(neighbour.b_lng),
            'image_icon': neighbour.image_icon
        })

    return res