from models.cellpose_service import CellposeProcessor

if __name__ == "__main__":
    # Processar imagem com Cellpose
    processor = CellposeProcessor()
    masks, flows, styles, diams = processor.process_image("/home/king/Downloads/microscopic.png")
