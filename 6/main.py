SOP_WIDTH = 4
SOM_WIDTH = 14

with open("6/input", "r", encoding = "UTF-8") as f:
    stream = f.read().strip()
    sop_packet = set()
    som_packet = set()
    sop_found = False
    som_found = False
    for i, packet in enumerate(stream):
        if not sop_found:
            j = i - len(sop_packet)
            while packet in sop_packet:
                sop_packet.remove(stream[j])
                j += 1

            sop_packet.add(packet)

            if len(sop_packet) == SOP_WIDTH:
                print(i + 1)
                sop_found = True

        if not som_found:
            j = i - len(som_packet)
            while packet in som_packet:
                som_packet.remove(stream[j])
                j += 1

            som_packet.add(packet)

            if len(som_packet) == SOM_WIDTH:
                print(i + 1)
                som_found = True

        if sop_found and som_found:
            break
