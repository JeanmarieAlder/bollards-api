from bollards_api.models import Bollard


"""
Get the position, number and name of the closest bollards 
(1no before, same no and 1no after)

@return an array of all neighbouring bollards
"""
def get_neighbours_by_number(current_bollard):
    current_number = current_bollard.b_number
    number_list = (
        current_number - 3,
        current_number - 2,
        current_number - 1, 
        current_number,
        current_number + 1,
        current_number + 2,
        current_number + 3
        )

    neighbours = Bollard.query.filter(Bollard.b_number.in_(number_list)).all()
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