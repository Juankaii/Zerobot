f"  ⚖️ Liquidez: ${pair['liquidity']['usd']:,.0f}\n"
                    f"  📈 Volumen 24h: ${pair['volume']['h24']:,.0f}\n"
                    f"  🕒 Creado: {datetime.fromtimestamp(pair['pairCreatedAt']/1000).strftime('%d/%m %H:%M')}\n\n"
                )

            await self.send_to_all(context, message)
            self.last_checked = datetime.now()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error API: {e}")
        except Exception as e:
            logger.exception("Error inesperado:")

    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        stats = (
            "📊 Estadísticas del Bot\n\n"
            f"👥 Usuarios activos: {len(self.active_users)}\n"
            f"⏱ Último check: {self.last_checked.strftime('%d/%m %H:%M') if self.last_checked else 'Nunca'}\n"
            f"🔔 Parámetros actuales:\n"
            f"  - Volumen mínimo: ${MIN_VOLUME:,.0f}\n"
            f"  - Liquidez mínima: ${MIN_LIQUIDITY:,.0f}\n"
            f"  - Máxima antigüedad: {MAX_AGE}h"
        )
        await update.message.reply_text(stats, parse_mode="Markdown")

async def main():
    analyzer = TokenAnalyzer()
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", analyzer.start))
    application.add_handler(CommandHandler("stats", analyzer.show_stats))
    
    # Configurar job periódico
    job_queue = application.job_queue
    job_queue.run_repeating(
        analyzer.check_opportunities,
        interval=CHECK_INTERVAL,
        first=10
    )
    
    # Iniciar bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Mantener el bot corriendo
    await application.updater.idle()

if name == "main":
    import asyncio
    asyncio.run(main())
