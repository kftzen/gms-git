import data_base as db  

if __name__ == "__main__":
    # # Está rutina convierte las aceleraciones en
    # # formato asa a un formato que permite una
    # # mayor velocidad de procesamiento.
    # lst_files = db.get_files()
    # for f in lst_files:
    #     print("Procesando archivo {}"\
    #         .format(f))
    #     df_ace = db.get_df(f)
    #     db.save_feather(df_ace,f)

    # # Está rutina convierte las aceleraciones en
    # # pseudo aceleraciones y genera el espectro
    # # del evento.
    # nm = db.Newmark()
    # pth_acce = nm.retrive_files()
    # for pth in pth_acce:
    #     nm.newmark_b(pth)
